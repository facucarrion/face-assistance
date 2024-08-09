export async function getSearchedPeople(query: string) {
    const response = await fetch(`http://127.0.0.1:8000/people/search?q=${query}`)
    const responseData = await response.json()
    return responseData
}