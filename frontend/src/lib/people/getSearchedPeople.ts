export async function getSearchedPeople(query: string, id_user: number) {
  const response = await fetch(
    `http://127.0.0.1:8000/people/search?q=${query}&id_user=${id_user}`
  )
  const responseData = await response.json()
  return responseData
}
