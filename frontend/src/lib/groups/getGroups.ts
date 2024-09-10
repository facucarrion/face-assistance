export async function getGroups(id_user: number) {
  const response = await fetch(
    `http://127.0.0.1:8000/groups?id_user=${id_user}`
  )
  const responseData = await response.json()
  return responseData
}
