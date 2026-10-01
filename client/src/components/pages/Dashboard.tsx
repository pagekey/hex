import AddWorkflowForm from "@/components/AddWorkflowForm";
import { Button } from "@/components/ui/button";
import WorkflowsList from "@/components/WorkflowsList";
import { checkLogin } from "@/lib/check";
import { getCurrentServer } from "@/lib/state";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
    const navigate = useNavigate();
    const handleLoginCheck = async () => {
        const server = getCurrentServer();
        if (!server) navigate("/login");
        const loggedIn = await checkLogin(server);
        if (!loggedIn) navigate("/login");
    };
    useEffect(() => {
        handleLoginCheck();
    }, []);

    const handleLogout = async () => {
        const server = getCurrentServer();

        if (!server) return;

        const request = await fetch(`${server}/sessions`, {
            method: "DELETE",
        });

        if (request.ok) {
            navigate("/")
        } else {
            alert("Logout failed unexpectedly.");
        }
    };
    return (
        <div>
            Dashboard!
            <Button onClick={handleLogout}>Logout</Button>
            <AddWorkflowForm />
            <WorkflowsList />
        </div>
    )
}
