export const checkLogin = async (server: string) => {
    try {
        const request = await fetch(`${server}/api/sessions/check`, {
            credentials: "include",  // Include cookies.
            headers: {
                "Content-Type": "application/json",
            },
        });
        if (request.ok) {
            const response = await request.json();
            return response.authenticated;
        } else {
            console.error("Error checking login.");
            return false;
        }
    } catch (error) {
        console.error("Error checking login:", error);
        return false;
    }
};
