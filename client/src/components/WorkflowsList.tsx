import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { getCurrentServer } from "@/lib/state";
import { useEffect, useState } from "react";

type Operation = {
    name: string;
    command: string;
};

type Workflow = {
    id: string;
    operations: Operation[];
};

export default function WorkflowsList() {
    const [workflows, setWorkflows] = useState<Workflow[]>([]);
    const [loading, setLoading] = useState(true);
    const [running, setRunning] = useState<string | null>(null);
    const [message, setMessage] = useState("");

    const loadWorkflows = async () => {
        try {
            const server = getCurrentServer();

            const request = await fetch(`${server}/api/workflows`, {
                credentials: "include",
            });

            const response = await request.json();
            setWorkflows(response);
        } catch (error) {
            setMessage("Failed to load workflows.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadWorkflows();
    }, []);

    const runWorkflow = async (id: string) => {
        setRunning(id);
        setMessage("");

        try {
            const server = getCurrentServer();

            const request = await fetch(
                `${server}/api/workflows/run`,
                {
                    method: "POST",
                    credentials: "include",
                    body: JSON.stringify({ id }),
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            const response = await request.json();
            setMessage(response.message);
        } catch (error) {
            setMessage("Failed to run workflow.");
        } finally {
            setRunning(null);
        }
    };

    if (loading) {
        return <Spinner />;
    }

    return (
        <div className="mx-auto w-full max-w-lg space-y-4">
            {message && <div>{message}</div>}

            {!workflows || workflows.length === 0 ? (
                <div>No workflows found.</div>
            ) : (
                <div className="space-y-2">
                    {workflows.map((workflow) => (
                        <div
                            key={workflow.id}
                            className="flex items-center justify-between rounded border p-3"
                        >
                            <div>
                                <div className="font-medium">
                                    {workflow.id}
                                </div>
                                <div className="text-sm text-muted-foreground">
                                    {workflow.operations.length} operation
                                    {workflow.operations.length !== 1
                                        ? "s"
                                        : ""}
                                </div>
                            </div>

                            <Button
                                onClick={() => runWorkflow(workflow.id)}
                                disabled={running !== null}
                            >
                                {running === workflow.id ? (
                                    <Spinner />
                                ) : (
                                    "Run"
                                )}
                            </Button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
