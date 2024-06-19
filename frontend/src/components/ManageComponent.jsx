import React, { useState } from 'react';
import UserForm from './userForm.jsx';


const ManageComponent = () => {
  const [view, setView] = useState('users');

  return (
    <div>
      <header className="flex justify-between items-center p-4 bg-gray-200">
        <h1 className="text-2xl mb-4">Gestionar Usuarios, Alumnos y Cursos</h1>
      </header>
      <main className="p-4">
        <div className="mb-8 flex space-x-4">
          <button
            onClick={() => setView('users')}
            className="bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Gestionar Usuarios
          </button>
          <button
            onClick={() => setView('groups')}
            className="bg-green-300 hover:bg-green-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Gestionar Cursos
          </button>
          <button
            onClick={() => setView('people')}
            className="bg-yellow-300 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Gestionar Alumnos
          </button>
        </div>

        {view === 'users' && <UserForm />}
        {view === 'groups' && <GroupForm />}
        {view === 'people' && <PersonForm />}
      </main>
    </div>
  );
};

export default ManageComponent;