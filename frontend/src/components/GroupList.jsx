import { useState, useEffect } from 'react'
import { getGroups } from '../lib/groups/getGroups'
import { verifyJwt } from '../lib/auth/jwt/verify'

export const GroupList = () => {
  const [groups, setGroups] = useState([])

  const fetchGroups = async () => {
    const user = await verifyJwt()
    const fetchedGroups = await getGroups(user.payload.id_user)
    setGroups(fetchedGroups)
  }

  useEffect(() => {
    fetchGroups()
  }, [])

  return (
    <ul id='groups-list' className='grid grid-cols-3 gap-4'>
      {groups.map(group => {
        return (
          <a href={`/groups/${group.id_group}`} key={group.id_group}>
            <li className='bg-white p-4 rounded-lg shadow-md cursor-pointer hover:bg-gray-200 transition transform hover:scale-105 text-center'>
              {group.name}
            </li>
          </a>
        )
      })}
    </ul>
  )
}
