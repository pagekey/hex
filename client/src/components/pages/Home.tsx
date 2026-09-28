import { Link } from "react-router-dom";

export default function Home() {
    return (
        <div>
            <div>
                Welcome to Hex!
            </div>
            <Link to="/login">Login</Link>
        </div>
    )
}
