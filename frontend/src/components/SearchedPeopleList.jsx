import { useState, useEffect } from 'react'
import { getSearchedPeople } from '../lib/people/getSearchedPeople'
import { verifyJwt } from '../lib/auth/jwt/verify'

export const SearchedPeopleList = ({ query }) => {
  const [searchedPeople, setSearchedPeople] = useState([])

  const fetchGroups = async () => {
    const user = await verifyJwt()
    const fetchedSearchedPeople = await getSearchedPeople(
      query,
      user.payload.id_user
    )
    setSearchedPeople(fetchedSearchedPeople)
  }

  useEffect(() => {
    fetchGroups()
  }, [])

  return (
    <ul id='groups-list' class='grid grid-cols-4 w-full gap-4'>
      {searchedPeople.length &&
        searchedPeople.map(person => {
          return (
            <a href={`/people/${person.id_person}`} key={person.id_person}>
              <li class='bg-white p-4 rounded-lg shadow-md cursor-pointer hover:bg-gray-200 transition transform hover:scale-105'>
                <p class='text-center text-black font-semibold text-lg'>
                  {person.firstname} {person.lastname}
                </p>
                <p class='text-center'>{person.document}</p>
                <p class='text-center'>{person.group_name}</p>
              </li>
            </a>
          )
        })}
    </ul>
  )
}
