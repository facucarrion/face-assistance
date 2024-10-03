import { useState, useEffect } from 'react'
import { getSearchedPeople } from '../lib/people/getSearchedPeople'
import { verifyJwt } from '../lib/auth/jwt/verify'

export const SearchedPeopleList = ({ query }) => {
  const [searchedPeople, setSearchedPeople] = useState([])

  const fetchPeople = async () => {
    const user = await verifyJwt()
    const fetchedSearchedPeople = await getSearchedPeople(
      query,
      user.payload.id_user
    )
    setSearchedPeople(fetchedSearchedPeople)
  }

  useEffect(() => {
    fetchPeople()
  }, [])

  return (
    searchedPeople.length ? (
      <ul id='groups-list' className='grid grid-cols-4 w-full gap-4'>

        {searchedPeople.map(person => {
          return (
            <a href={`/people/${person.id_person}`} key={person.id_person}>
              <li className='bg-white p-4 rounded-lg shadow-md cursor-pointer hover:bg-gray-200 transition transform hover:scale-105'>
                <p className='text-center text-black font-semibold text-lg'>
                  {person.firstname} {person.lastname}
                </p>
                <p className='text-center'>{person.document}</p>
                <p className='text-center'>{person.group_name}</p>
              </li>
            </a>
          )
        })}
      </ul>
    ) : <p>{`No se encontraron resultados para tu búsqueda "${query}"`}</p>
  )
}
