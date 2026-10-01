import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Spinner } from "@/components/ui/spinner";
import { setCurrentServer } from "@/lib/state";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const navigate = useNavigate();

    const [loading, setLoading] = useState<boolean>(false);
    const [message, setMessage] = useState<string>("");

    const [server, setServer] = useState<string>("");
    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    const onSubmit = async (e: any) => {
        e.preventDefault();
        setLoading(false);
        try {
            const request = await fetch(`${server}/api/sessions`, {
                method: "POST",
                body: JSON.stringify({
                    username,
                    password,
                }),
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
            });
            if (request.status == 201) {
                setCurrentServer(server);
                navigate("/dashboard");
            } else {
                const response = await request.json();
                setMessage(response.message);
            }
        } catch (error) {
            setMessage("An unexpected error occurred.");
        } finally {
            setLoading(false);
        }
    }

    if (loading) return <Spinner />;

    return (
        <form className="mx-auto w-full max-w-sm space-y-4" onSubmit={onSubmit}>
            <div className="text-red-600">{message}</div>
            <div>
                <Label htmlFor="server">Server</Label>
                <Input id="server" name="server" onChange={(e) => setServer(e.target.value)} />
            </div>

            <div>
                <Label htmlFor="username">Username</Label>
                <Input id="username" name="username" onChange={(e) => setUsername(e.target.value)} />
            </div>

            <div>
                <Label htmlFor="password">Password</Label>
                <Input id="password" name="password" type="password" onChange={(e) => setPassword(e.target.value)} />
            </div>

            <Button type="submit" className="w-full">
                Log in
            </Button>
        </form>
    )
}
