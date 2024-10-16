import { useNavigate } from "react-router-dom";
import { logout_user } from "../../utils/api";

const Header = ({ showVechileDialog, setShowVehicleDialog }) => {
    const navigate = useNavigate();
    return <div className="navbar bg-base-100 border-b-2 border-gray-200 px-8 flex">
        <a className="btn btn-ghost text-xl">Welcome to Sonnet</a>
        <button className='btn btn-sm btn-neutral ml-auto' onClick={async () => {
            setShowVehicleDialog(showVechileDialog ? false : true);
        }}>Manage vehicle</button>
        <button className='btn btn-sm btn-neutral ml-8' onClick={async () => {
            logout_user();
            navigate('/')
        }}>Logout</button>
    </div>
}
export default Header;