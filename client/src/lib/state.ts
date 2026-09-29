export const setCurrentServer = (server: string) => {
    localStorage.setItem("current_server", server);
};
export const getCurrentServer = () => {
    return localStorage.getItem("current_server") || "";
}
