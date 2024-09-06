export const getMonthlyAssistance = async (
  id_person: number,
  month: number,
  year: number = new Date().getFullYear()
) => {
  const response = await fetch(
    `http://127.0.0.1:8000/people/${id_person}/assistance/${year}/${month}/`
  )
  const data = await response.json()
  return data
}
