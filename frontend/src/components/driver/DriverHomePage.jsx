import { useEffect, useState } from 'react';
import DrivesTable from './DrivesTable';
import { getRides } from '../../utils/api';
import Header from '../common/Header';
import VehicleDialog from './AddOrUpdateVehicle';

export const DriverHomePage = () => {
    const [drives, setDrives] = useState(null);
    const [showVehicleDialog, setShowVehicleDialog] = useState(false);
    useEffect(() => {
        async function fetchData() {
            const _drives = await getRides();
            setDrives(_drives);
        }
        fetchData();
    }, []);
    console.log(showVehicleDialog)
    return (
        <>
            {showVehicleDialog ? <VehicleDialog setShowVehicleDialog={setShowVehicleDialog} /> : <div></div>}
            <Header showVehicleDialog={showVehicleDialog} setShowVehicleDialog={setShowVehicleDialog} />
            {drives ? <DrivesTable drives={drives} /> : <div>Not found</div>}
        </>
    );
};
