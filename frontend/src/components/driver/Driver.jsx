import { Routes, Route } from 'react-router-dom';
import DriverHomePage from './DriverHomePage';
import UserInfo from './UserInfo';
import RideRequestDialog from './RideRequestDialog';
import { useEffect, useState } from 'react';
import { ACCESS_TOKEN_STORAGE_KEY } from '../../config';

export const Driver = () => {
    const data = {
        "pickupLocation": "30495 Samantha Plains\nSouth Mary, CA 87658",
        "dropoffLocation": "12036 Jayne Roads\nNew John, MT 77877",
        "distance": 34.76,
        "estimatedTime": 62,
        "fare": 85.45,
        "passengerName": "Ronald Johnson",
        "passengerContact": "(613) 951-7163"
    }
    const [rideDetails, setRideDetails] = useState(null);
    const requestOptions = {
        method: "GET",
        redirect: "follow"
    };
    const token = localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY)
    const eventSource = new EventSource(`http://0.0.0.0:8000/api/v1/drivers/new_ride?token=${token}`);

    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("Received data:", data);
    };

    eventSource.onerror = (error) => {
        console.error("SSE Error:", error);
    };

    const [open, setOpen] = useState(true);
    function onAccept() {
        setRideDetails(null)
        setOpen(false)
    }
    function onDecline() {
        setRideDetails(null)
        setOpen(false)

    }
    return (
        <>
            <RideRequestDialog open={open} onDecline={onDecline} onAccept={onAccept} rideDetails={data} />
            <Routes>
                <Route path="homepage/*" element={<DriverHomePage />} />
            </Routes>
        </>
    );
};
