import { useState, useEffect } from 'react'

const UserForm = () => {
  const [users, setUsers] = useState([])
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    id_rol: 0
  })

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/users/')
      const usersData = await response.json()
      setUsers(usersData)
    } catch (error) {
      console.error('Error fetching users:', error)
    }
  }

  useEffect(() => {
    fetchUsers()
  }, [])

  useEffect(() => {
    console.log(users)
  }, [users])

  const handleCreateUser = async event => {
    event.preventDefault()

    try {
      const response = await fetch('http://127.0.0.1:8000/users/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        alert('User created successfully!')
        fetchUsers()
      } else {
        alert('Failed to create user')
      }
    } catch (error) {
      console.error('Error creating user:', error)
    }
  }

  const handleDeleteUser = async id_user => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/users/${id_user}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        alert('User deleted successfully!')
        fetchUsers()
      } else {
        alert('Failed to delete user')
      }
    } catch (error) {
      console.error('Error deleting user:', error)
    }
  }

  const handleChange = event => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value
    })
  }

  return (
    <div className='max-w-md mx-auto mt-10'>
      <h2 className='text-2xl font-bold mb-4'>Crear Usuario</h2>
      <form
        onSubmit={userToEdit ? handleUpdateUser : handleCreateUser}
        className='bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4'
      >
        <div className='mb-4'>
          <label
            htmlFor='username'
            className='block text-gray-700 text-sm font-bold mb-2'
          >
            Nombre de Usuario:
          </label>
          <input
            className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
            type='text'
            name='username'
            id='username'
            placeholder='Ingrese el nombre de usuario'
            required
            value={formData.username}
            onChange={handleChange}
          />
        </div>

        <div className='mb-4'>
          <label
            htmlFor='password'
            className='block text-gray-700 text-sm font-bold mb-2'
          >
            Contraseña:
          </label>
          <input
            className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
            type='password'
            name='password'
            id='password'
            placeholder='Ingrese la contraseña'
            value={formData.password}
            onChange={handleChange}
          />
        </div>

        <div className='mb-4'>
          <label
            htmlFor='password'
            className='block text-gray-700 text-sm font-bold mb-2'
          >
            Confirmar Contraseña:
          </label>
          <input
            className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
            type='password'
            name='repeat_password'
            id='repeat_ password'
            placeholder='Confirmar contraseña'
            value={formData.repeat_password}
            onChange={handleChange}
          />
        </div>

        <div className='mb-4'>
          <label
            htmlFor='id_rol'
            className='block text-gray-700 text-sm font-bold mb-2'
          >
            Rol:
          </label>
          <input
            className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
            type='number'
            id='id_rol'
            name='id_rol'
            placeholder='Ingrese el rol'
            required
            value={formData.id_rol}
            onChange={handleChange}
          />
        </div>

        <button
          type='submit'
          className='bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
        >
          {userToEdit ? 'Actualizar Usuario' : 'Crear Usuario'}
        </button>
        {userToEdit && (
          <button
            type='button'
            className='bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
            onClick={() => {
              setUserToEdit(null)
              setFormData({
                username: '',
                password: '',
                repeat_password: '',
                id_rol: 0
              })
            }}
          >
            Limpiar
          </button>
        )}
      </form>

      <h2 className='text-xl mb-2'>Lista de Usuarios</h2>
      <table className='min-w-full bg-white shadow-md rounded'>
        <thead>
          <tr>
            <th className='py-2'>ID</th>
            <th className='py-2'>Username</th>
            <th className='py-2'>Rol</th>
            <th className='py-2'>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id_user}>
              <td className='py-2'>{user.id_user}</td>
              <td className='py-2'>{user.username}</td>
              <td className='py-2'>{user.rol}</td>
              <td className='py-2'>
                <button
                  onClick={() => handleDeleteUser(user.id_user)}
                  className='bg-red-300 hover:bg-red-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                >
                  Eliminar
                </button>
                <button
                  onClick={() => handleUpdateUser(user.id_user)}
                  className='bg-yellow-300 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                >
                  Editar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
export default UserForm
