
import React from 'react';
import CustomMap from './CustomMap';
import { Route, Routes } from 'react-router-dom';

const VehicleInfo = ({ vehicle }) => {
    return (
        <div className="p-6 max-w-xl mx-auto bg-white shadow-lg rounded-lg border border-gray-200">
            <h1 className="text-2xl font-bold mb-4 text-center">Vehicle Information</h1>

            <div className="mb-6">
                <h2 className="text-lg font-semibold mb-2 text-gray-700">License & Registration</h2>
                <p className="text-gray-600"><strong>License Number:</strong> {vehicle.license_number}</p>
                <p className="text-gray-600"><strong>Registration Number:</strong> {vehicle.registration_number}</p>
            </div>

            <div className="mb-6">
                <h2 className="text-lg font-semibold mb-2 text-gray-700">Capacity</h2>
                <p className="text-gray-600"><strong>Capacity:</strong> {vehicle.capacity}</p>
            </div>

            <div className="mb-6">
                <h2 className="text-lg font-semibold mb-2 text-gray-700">Driver Information</h2>
                <p className="text-gray-600"><strong>Driver Name:</strong> {vehicle.driver.name}</p>
                <p className="text-gray-600"><strong>Driver ID:</strong> {vehicle.driver.id}</p>
                <p className="text-gray-600"><strong>Created At:</strong> {new Date(vehicle.driver.created_at).toLocaleString()}</p>
                <p className="text-gray-600"><strong>Updated At:</strong> {new Date(vehicle.driver.updated_at).toLocaleString()}</p>
            </div>

            <div className="mb-6">
                <h2 className="text-lg font-semibold mb-2 text-gray-700">Location</h2>
                <p className="text-gray-600"><strong>Additional Prop 1:</strong> {vehicle.location.additionalProp1}</p>
                <p className="text-gray-600"><strong>Additional Prop 2:</strong> {vehicle.location.additionalProp2}</p>
                <p className="text-gray-600"><strong>Additional Prop 3:</strong> {vehicle.location.additionalProp3}</p>
            </div>
        </div>
    );
};
const DrivesComp = ({ drives }) => {
    return <div className="overflow-x-auto px-24">
        <table className="table w-full">
            <thead>
                <tr>
                    <th>Status</th>
                    <th>Driver ID</th>
                    <th>Drive ID</th>
                    <th>User Name</th>
                    <th>User ID</th>
                    <th>Created At</th>
                    <th>Updated At</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {drives.map((drive) => (
                    <tr key={drive.id}>
                        <td>{drive.status}</td>
                        <td>{drive.driver_id}</td>
                        <td>{drive.id}</td>
                        <td>{drive.user.name}</td>
                        <td>{drive.user.id}</td>
                        <td>{new Date(drive.created_at).toLocaleString()}</td>
                        <td>{new Date(drive.updated_at).toLocaleString()}</td>
                        <td><a href={`/homepage/${drive.id}`} className='btn btn-neutral'> View</a></td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}



export const DriverHomePage = () => {

    const drives = [
        {
            "status": "accepted",
            "driver_id": "NRcxo4qpYRKJ",
            "id": "Ge22jnOBqqcx",
            "user": {
                "name": "Saurabh",
                "id": "Fg1XUGO4e2yv",
                "created_at": "2024-10-15T09:09:09.492708Z",
                "updated_at": "2024-10-15T09:09:09.492712Z"
            },
            "created_at": "2024-10-15T09:27:00.747798Z",
            "updated_at": "2024-10-15T09:27:00.747802Z"
        },
        {
            "status": "accepted",
            "driver_id": "NRcxo4qpYRKJ",
            "id": "oEvHtJ2qocGj",
            "user": {
                "name": "Saurabh",
                "id": "Fg1XUGO4e2yv",
                "created_at": "2024-10-15T09:09:09.492708Z",
                "updated_at": "2024-10-15T09:09:09.492712Z"
            },
            "created_at": "2024-10-15T09:27:42.633791Z",
            "updated_at": "2024-10-15T09:27:42.633794Z"
        },
        {
            "status": "accepted",
            "driver_id": "NRcxo4qpYRKJ",
            "id": "TdYiB8abRVFc",
            "user": {
                "name": "Saurabh",
                "id": "Fg1XUGO4e2yv",
                "created_at": "2024-10-15T09:09:09.492708Z",
                "updated_at": "2024-10-15T09:09:09.492712Z"
            },
            "created_at": "2024-10-15T09:28:02.360778Z",
            "updated_at": "2024-10-15T09:28:02.360782Z"
        },
        {
            "status": "accepted",
            "driver_id": "NRcxo4qpYRKJ",
            "id": "iIMCVhD89PoF",
            "user": {
                "name": "Saurabh",
                "id": "Fg1XUGO4e2yv",
                "created_at": "2024-10-15T09:09:09.492708Z",
                "updated_at": "2024-10-15T09:09:09.492712Z"
            },
            "created_at": "2024-10-15T09:28:18.030762Z",
            "updated_at": "2024-10-15T09:28:18.030766Z"
        }
    ]

    return <>
        <div className="navbar bg-base-100 border-b-2 flex flex-col border-gray-200">
            <a className="btn btn-ghost text-xl">Welcome to Sonnet</a>
        </div>
        <DrivesComp drives={drives} />
    </>
}


const UserInfo = () => {
    const vehicleData = {
        license_number: "ABC12345",
        registration_number: "REG67890",
        capacity: 4,
        driver_id: "DRIVER001",
        location: {
            additionalProp1: 40.7128,  // Latitude
            additionalProp2: -74.0060, // Longitude
            additionalProp3: 100,      // Altitude or any other data
        },
        driver: {
            name: "John Doe",
            id: "DRIVER001",
            created_at: "2024-10-15T07:53:47.486Z",
            updated_at: "2024-10-15T08:00:47.486Z"
        }
    };
    return <div className=' w-full flex md:flex-col lg:flex-row mt-24 [&>*]:w-1/2 items-center justify-center'>
        < VehicleInfo vehicle={vehicleData} />
        <div className='md:w-full'>
            <CustomMap />
        </div>
    </div>
}
export const UserPage = () => {
    return <>
        <div className="navbar bg-base-100 border-b-2 border-gray-200 flex flex-col">
            <a className="btn btn-ghost text-xl">Welcome to Sonnet</a>
        </div>
        <UserInfo />
    </>
}