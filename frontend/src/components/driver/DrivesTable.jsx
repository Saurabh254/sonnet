
const DrivesTable = ({ drives }) => (
    <div className="overflow-x-auto px-24">
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
                        <td>{drive.driverId}</td>
                        <td>{drive.id}</td>
                        <td>{drive.user.name}</td>
                        <td>{drive.user.id}</td>
                        <td>{new Date(drive.createdAt).toLocaleString()}</td>
                        <td>{new Date(drive.updatedAt).toLocaleString()}</td>
                        <td><a href={`/homepage/${drive.id}`} className='btn btn-neutral btn-sm'> View</a></td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
);

export default DrivesTable;
