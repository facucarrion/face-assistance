import React, { useState } from 'react'
import UserForm from './userForm.jsx'
import GroupsForm from './groupsForm.jsx'
import PeopleForm from './peopleForm.jsx'

const ManageComponent = () => {
  const [view, setView] = useState('users')

  return (
    <div>
      <header className='flex justify-between items-center p-4 bg-gray-200'>
        <div className='flex items-center'>
          <img src='/logo.svg' alt='Logo' className='h-20 ml-4' />
        </div>
      </header>
      <main className='p-4'>
        <div className='flex items-center mb-4'>
          <a href='/homepage' className='flex items-center'>
            <svg
              xmlns='http://www.w3.org/2000/svg'
              className='h-6 w-6 mr-2'
              viewBox='0 0 20 20'
              fill='currentColor'
            >
              <path
                fillRule='evenodd'
                d='M12.707 5.293a1 1 0 010 1.414L9.414 10H17a1 1 0 110 2h-7.586l3.293 3.293a1 1 0 01-1.414 1.414l-5-5a1 1 0 010-1.414l5-5a1 1 0 011.414 0z'
                clipRule='evenodd'
              />
            </svg>
          </a>
          <h1 className='text-2xl ml-4'>Panel de Gestión</h1>
        </div>
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
        </div>

        {view === 'users' && <UserForm />}
        {view === 'groups' && <GroupsForm />}
        {view === 'people' && <PeopleForm />}
      </main>
    </div>
  )
}

export default ManageComponent
