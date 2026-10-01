import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Spinner } from "@/components/ui/spinner";
import { getCurrentServer } from "@/lib/state";
import { useState } from "react";

type Operation = {
    name: string;
    command: string;
};

export default function AddWorkflowForm() {
    const [loading, setLoading] = useState<boolean>(false);
    const [message, setMessage] = useState<string>("");

    const [id, setId] = useState("");
    const [operations, setOperations] = useState<Operation[]>([]);

    const addOperation = () => {
        setOperations([...operations, { name: "", command: "" }]);
    };

    const removeOperation = (index: number) => {
        setOperations(operations.filter((_, i) => i !== index));
    };

    const updateOperation = (
        index: number,
        field: keyof Operation,
        value: string
    ) => {
        setOperations(
            operations.map((operation, i) =>
                i === index ? { ...operation, [field]: value } : operation
            )
        );
    };

    const onSubmit = async (e: any) => {
        e.preventDefault();
        setLoading(false);
        try {
            const server = getCurrentServer();
            const request = await fetch(`${server}/api/workflows`, {
                method: "POST",
                body: JSON.stringify({
                    id,
                    operations,
                }),
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
            });
            const response = await request.json();
            setMessage(response.message);
        } catch (error) {
            setMessage("An unexpected error occurred.");
        } finally {
            setLoading(false);
        }
    }

    if (loading) return <Spinner />;

    return (
        <form className="mx-auto w-full max-w-lg space-y-4" onSubmit={onSubmit}>
            <div>{message}</div>
            <div>
                <Label htmlFor="id">Workflow ID</Label>
                <Input
                    id="id"
                    name="id"
                    value={id}
                    onChange={(e) => setId(e.target.value)}
                />
            </div>

            <div className="space-y-3">
                <div className="flex items-center justify-between">
                    <Label>Operations</Label>

                    <Button
                        type="button"
                        size="icon"
                        variant="outline"
                        onClick={addOperation}
                    >
                        +
                    </Button>
                </div>

                {operations.map((operation, index) => (
                    <div key={index} className="flex gap-2">
                        <Input
                            placeholder="Name"
                            value={operation.name}
                            onChange={(e) =>
                                updateOperation(index, "name", e.target.value)
                            }
                        />

                        <Input
                            placeholder="Command"
                            value={operation.command}
                            onChange={(e) =>
                                updateOperation(index, "command", e.target.value)
                            }
                        />

                        <Button
                            type="button"
                            variant="outline"
                            onClick={() => removeOperation(index)}
                        >
                            -
                        </Button>
                    </div>
                ))}
            </div>

            <Button type="submit" className="w-full">
                Add Workflow
            </Button>
        </form>
    );
}
