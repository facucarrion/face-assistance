export async function getPerson(id_person: string) {
    const response = await fetch(`http://127.0.0.1:8000/people/${id_person}`)
    const responseData = await response.json()
    return responseData
}