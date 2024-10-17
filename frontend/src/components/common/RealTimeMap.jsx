import React, { useState, useEffect, useRef } from 'react';
import { GoogleMap, Marker, DirectionsRenderer } from '@react-google-maps/api';
import { useJsApiLoader } from '@react-google-maps/api';
import MarkerCar from '../../assets/car_top_view.png'; // Custom marker image
import { ACCESS_TOKEN_STORAGE_KEY, BASE_WEBSOCKET_URL, GOOGLE_MAPS_API_KEY } from '../../config';

const containerStyle = {
    width: '100%',
    height: '400px',
};

function RealTimeMap({ location_b, endpoint }) {
    const [location_a, setLocationA] = useState({ lat: null, lng: null }); // Start with null values
    const [directionsResponse, setDirectionsResponse] = useState(null);

    const center = React.useMemo(() => {
        if (!location_a || !location_b) return null;

        // Calculate the average of latitude and longitude to get the center
        const lat = (location_a.lat + location_b.lat) / 2;
        const lng = (location_a.lng + location_b.lng) / 2;

        return { lat, lng };
    }, [location_a, location_b]);



    const { isLoaded } = useJsApiLoader({
        id: 'google-map-script',
        googleMapsApiKey: GOOGLE_MAPS_API_KEY, // Add your Google Maps API Key here
    });

    const [map, setMap] = useState(null);
    const websocketRef = useRef(null); // Reference for the WebSocket connection

    const onLoad = React.useCallback(function callback(map) {
        const bounds = new window.google.maps.LatLngBounds(center);
        map.fitBounds(bounds);
        setMap(map);
    }, [center]);

    const onUnmount = React.useCallback(function callback(map) {
        setMap(null);
    }, []);

    // Establish WebSocket connection on component mount and listen for location updates
    useEffect(() => {
        const ws = new WebSocket(`${BASE_WEBSOCKET_URL}/${endpoint}`);
        websocketRef.current = ws;

        ws.onopen = () => {
            const _token = localStorage.get(ACCESS_TOKEN_STORAGE_KEY)
            ws.send(_token)
            print(_token)
            console.log('WebSocket connected');
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                // Expecting data to have format: { lat: number, lng: number }
                if (data.lat !== null && data.lng !== null) {
                    setLocationA({ lat: data.lat, lng: data.lng }); // Update location_a
                }
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };

        ws.onclose = () => {
            console.log('WebSocket disconnected');
        };

        ws.onerror = (err) => {
            console.error('WebSocket error:', err);
        };

        return () => {
            if (ws) {
                ws.close(); // Close WebSocket on component unmount
            }
        };
    }, []);

    // Request directions between markerA (location_a) and location_b
    useEffect(() => {
        if (isLoaded && location_a.lat && location_a.lng && location_b.lat && location_b.lng) {
            const directionsService = new window.google.maps.DirectionsService();
            directionsService.route(
                {
                    origin: location_a,
                    destination: location_b,
                    travelMode: window.google.maps.TravelMode.DRIVING,
                },
                (result, status) => {
                    if (status === 'OK') {
                        setDirectionsResponse(result);
                    } else {
                        console.error(`Error fetching directions: ${status}`);
                    }
                }
            );
        }
    }, [isLoaded, location_a, location_b]);

    return isLoaded ? (
        <GoogleMap
            mapContainerStyle={containerStyle}
            center={center}
            zoom={10}
            onUnmount={onUnmount}
        >
            {/* Marker B */}
            <Marker position={location_b} />

            {/* Marker for the current location (location_a) with a custom icon */}
            {location_a.lat && location_a.lng && (
                <Marker
                    position={location_a}
                    icon={{
                        url: MarkerCar, // Custom image URL for car icon
                        scaledSize: new window.google.maps.Size(50, 50), // Adjust size
                    }}
                />
            )}

            {/* Show the directions between markerA and markerB */}
            {directionsResponse && (
                <DirectionsRenderer directions={directionsResponse} />
            )}
        </GoogleMap>
    ) : <></>;
}

export default RealTimeMap;
