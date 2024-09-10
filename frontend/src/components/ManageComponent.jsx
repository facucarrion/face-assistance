import { useState } from 'react'

import UserForm from './userForm.jsx'
import GroupsForm from './groupsForm.jsx'
import PeopleForm from './peopleForm.jsx'
import ScheduleForm from './scheduleForm.jsx'

const ManageComponent = () => {
  const [view, setView] = useState('users')

  return (
    <div>
      <div className='mb-8 flex space-x-4'>
        <button
          onClick={() => setView('users')}
          className='bg-gray-300 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
        >
          Gestionar Usuarios
        </button>
        <button
          onClick={() => setView('groups')}
          className='bg-gray-300 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
        >
          Gestionar Cursos
        </button>
        <button
          onClick={() => setView('people')}
          className='bg-gray-300 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
        >
          Gestionar Alumnos
        </button>
        <button
          onClick={() => setView('schedules')}
          className='bg-gray-300 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
        >
          Gestionar Horarios
        </button>
      </div>

      <div className='grid grid-cols-2 gap-8'>
        {view === 'users' && <UserForm />}
        {view === 'groups' && <GroupsForm />}
        {view === 'people' && <PeopleForm />}
        {view === 'schedules' && <ScheduleForm />}
      </div>
    </div>
  )
}

export default ManageComponent
