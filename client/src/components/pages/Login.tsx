import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function Login() {
    const onSubmit = (e: any) => {
        e.preventDefault();
        console.log("hi!");
        // API request here!
    }
    return (
        <form className="mx-auto w-full max-w-sm space-y-4" onSubmit={onSubmit}>
            <div>
                <Label htmlFor="server">Server</Label>
                <Input id="server" name="server" />
            </div>

            <div>
                <Label htmlFor="username">Username</Label>
                <Input id="username" name="username" />
            </div>

            <div>
                <Label htmlFor="password">Password</Label>
                <Input id="password" name="password" type="password" />
            </div>

            <Button type="submit" className="w-full">
                Log in
            </Button>
        </form>
    )
}
