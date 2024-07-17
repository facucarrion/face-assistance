export async function getGroup(id_group) {
    const response = await fetch(`http://127.0.0.1:8000/groups/${id_group}`)
    const responseData = await response.json()
    return responseData
}