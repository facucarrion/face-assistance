import { useState, useEffect } from 'react'

const UserForm = () => {
  const [users, setUsers] = useState([])
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    repeat_password: '',
    id_rol: 0
  })
  const [userToEdit, setUserToEdit] = useState(null)
  const [roles, setRoles] = useState([])
  const [selectedRole, setSelectedRole] = useState(null)

  const fetchUsers = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/users/')
      const usersData = await response.json()
      setUsers(usersData)
    } catch (error) {
      console.error('Error al recuperar usuarios:', error)
    }
  }

  const fetchRoles = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/users/roles/')
      const rolesData = await response.json()
      setRoles(rolesData)
    } catch (error) {
      console.error('Error al recuperar roles:', error)
    }
  }

  useEffect(() => {
    fetchUsers()
    fetchRoles()
  }, [])

  useEffect(() => {
    if (userToEdit) {
      setFormData({
        username: userToEdit.username,
        password: '',
        repeat_password: '',
        id_rol: userToEdit.id_rol
      })
    }
  }, [userToEdit])

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
        alert('¡Usuario creado exitosamente!')
        fetchUsers()
        setFormData({
          username: '',
          password: '',
          repeat_password: '',
          id_rol: 0
        })
      } else {
        alert('No se pudo crear el usuario')
      }
    } catch (error) {
      console.error('Error al crear usuario:', error)
    }
  }

  const handleDeleteUser = async id_user => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/users/${id_user}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        alert('¡Usuario eliminado exitosamente!')
        fetchUsers()
      } else {
        alert('No se pudo eliminar el usuario')
      }
    } catch (error) {
      console.error('Error al eliminar usuario:', error)
    }
  }

  const handleUpdateUser = async event => {
    event.preventDefault()

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/users/${userToEdit.id_user}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        }
      )

      if (response.ok) {
        alert('¡Usuario actualizado exitosamente!')
        fetchUsers()
        setUserToEdit(null)
        setFormData({
          username: '',
          password: '',
          repeat_password: '',
          id_rol: 0
        })
      } else {
        alert('No se pudo actualizar el usuario')
      }
    } catch (error) {
      console.error('Error al actualizar usuario:', error)
    }
  }

  const handleChange = event => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value
    })
  }

  return (
    <div className='container mx-auto mt-10 flex'>
      <div className='w-1/2 pr-4'>
        <h2 className='text-2xl font-bold mb-4'>
          {userToEdit ? 'Editar Usuario' : 'Crear Usuario'}
        </h2>
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
              required
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
              required
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
            <select
              className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
              name='id_rol'
              id='id_rol'
              value={formData.id_rol}
              onChange={handleChange}
              required
            >
              {roles.map(role => (
                <option key={role.id_rol} value={role.id_rol}>
                  {role.rol}
                </option>
              ))}
            </select>
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
      </div>

      <div className='w-1/2 pl-4'>
        <h2 className='text-2xl font-bold mb-4'>Lista de Usuarios</h2>
        <div className='max-h-96 overflow-y-auto'>
          <table className='min-w-full bg-white shadow-md rounded mb-4'>
            <thead>
              <tr>
                <th className='py-2 px-4 bg-gray-200 text-left'>Username</th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Rol</th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {users.map(user => (
                <tr key={user.id_user}>
                  <td className='py-2 px-4 border-b'>{user.username}</td>
                  <td className='py-2 px-4 border-b'>{user.rol}</td>
                  <td className='py-2 px-4 border-b flex space-x-2'>
                    <button
                      onClick={() => handleDeleteUser(user.id_user)}
                      className='bg-red-300 hover:bg-red-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                    >
                      Eliminar
                    </button>

                    <button
                      onClick={() => {
                        setUserToEdit(user)
                      }}
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
      </div>
    </div>
  )
}
export default UserForm
