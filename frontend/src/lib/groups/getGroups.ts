export async function getGroups() {
    const response = await fetch("http://127.0.0.1:8000/groups")
    const responseData = await response.json()
    return responseData
}