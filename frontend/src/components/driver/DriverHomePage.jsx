import { useEffect, useState } from 'react';
import DrivesTable from './DrivesTable';
import { getRides } from '../../utils/api';
import Header from '../common/Header';

export const DriverHomePage = () => {
    const [drives, setDrives] = useState(null);

    useEffect(() => {
        async function fetchData() {
            const _drives = await getRides();
            setDrives(_drives);
        }
        fetchData();
    }, []);

    return (
        <>
            <Header />
            {drives ? <DrivesTable drives={drives} /> : <div>Not found</div>}
        </>
    );
};
