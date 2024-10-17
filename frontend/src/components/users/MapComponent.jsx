import { GoogleMap, LoadScript, Marker, DirectionsRenderer } from '@react-google-maps/api';
import { GOOGLE_MAPS_API_KEY } from '../../config';


const MapComponent = ({ location, allVehicles, onMapClick }) => {
    const mapContainerStyle = {
        height: '400px',
        width: '100%',
    };

    const center = {
        lat: location.lat,
        lng: location.lng,
    };

    console.log('Pickup Location:', location);
    console.log('All Vehicles:', allVehicles); // Log vehicles to check their data

    return (
        <LoadScript googleMapsApiKey={GOOGLE_MAPS_API_KEY}>
            <GoogleMap
                mapContainerStyle={mapContainerStyle}
                center={center}
                zoom={15}
                onClick={onMapClick}
            >
                {/* Marker for pickup location */}
                <Marker position={location} label="Pickup" />

                {/* Markers for all vehicles */}
                {allVehicles.map((vehicle) => {
                    console.log('Vehicle:', vehicle); // Log each vehicle
                    return (
                        <Marker
                            key={vehicle.vehicle_id} // Ensure this matches your vehicle ID property
                            position={{
                                lat: vehicle.location.latitude,
                                lng: vehicle.location.longitude,
                            }}
                            label={{
                                text: vehicle.driver.name, // Use vehicle name as label
                                color: "black", // Change the color of the label
                            }}// Use vehicle name as label
                        />
                    );
                })}
            </GoogleMap>
        </LoadScript>
    );
};



// export const ShowDistanceMapComponent = ({ location, dropOffLocation, onMapClick }) => {
//     const mapContainerStyle = {
//         height: '400px',
//         width: '100%',
//     };

//     const center = {
//         lat: location.lat,
//         lng: location.lng,
//     };

//     return (
//         <LoadScript googleMapsApiKey={GOOGLE_MAPS_API_KEY} libraries={['places']}>
//             <GoogleMap
//                 mapContainerStyle={mapContainerStyle}
//                 center={center}
//                 zoom={15}
//                 onClick={onMapClick}
//             >
//                 {/* Marker for pickup location */}
//                 <Marker position={location} label="Pickup" />

//                 {/* Marker for drop-off location */}
//                 <Marker position={dropOffLocation} label="Drop-off" />
//             </GoogleMap>
//         </LoadScript>
//     );
// };



export default MapComponent;
