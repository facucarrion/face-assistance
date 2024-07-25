import React, { useState } from 'react';
import UserForm from './userForm.jsx';
import GroupsForm from './groupsForm.jsx';
import PeopleForm from './peopleForm.jsx';

const ManageComponent = () => {
  const [view, setView] = useState('users');

  return (
    <div>
      <header className="flex justify-between items-center p-4 bg-gray-200">
        <div className="flex items-center">
          <img src="/logo.svg" alt="Logo" className="h-20 ml-4" />
          <a href="/homepage">
            <button
              className="bg-gray-200 text-black font-semibold px-4 py-2 rounded-lg hover:bg-gray-400"
            >
              Volver a Inicio
            </button>
          </a>
        </div>
      </header>   
      <main className="p-4">
      <h1 className="text-2xl mb-4">Panel de Gestión</h1>
        <div className="mb-8 flex space-x-4">
          <button
            onClick={() => setView('users')}
            className="bg-gray-300 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Gestionar Usuarios
          </button>
          <button
            onClick={() => setView('groups')}
            className="bg-gray-300 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Gestionar Cursos
          </button>
          <button
            onClick={() => setView('people')}
            className="bg-gray-300 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Gestionar Alumnos
          </button>
        </div>

        {view === 'users' && <UserForm />}
        {view === 'groups' && <GroupsForm />}
        {view === 'people' && <PeopleForm />}
      </main>
    </div>
  );
};

export default ManageComponent;