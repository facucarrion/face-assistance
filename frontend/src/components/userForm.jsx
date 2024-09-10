import { useState, useEffect } from 'react'

const UserForm = () => {
  const [users, setUsers] = useState([])
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    repeat_password: '',
    id_rol: 1
  })
  const [userToEdit, setUserToEdit] = useState(null)
  const [roles, setRoles] = useState([])

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

    if (!formData.password) {
      alert('La contraseña es obligatoria al crear un usuario')
      return
    }

    if (formData.password !== formData.repeat_password) {
      alert('Las contraseñas no coinciden')
      return
    }

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
          id_rol: 1
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

    if (formData.password && formData.password !== formData.repeat_password) {
      alert('Las contraseñas no coinciden')
      return
    }

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
          id_rol: 1
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
    <>
      <div className='w-full'>
        <h2 className='text-2xl font-bold mb-4'>
          {userToEdit ? 'Editar Usuario' : 'Crear Usuario'}
        </h2>
        <form
          onSubmit={userToEdit ? handleUpdateUser : handleCreateUser}
          className='bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 h-[450px] flex flex-col justify-between'
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
              required={!!formData.password}
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

          <div className='grid grid-cols-2 gap-4'>
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
          </div>
        </form>
      </div>

      <div className='w-full'>
        <h2 className='text-2xl font-bold mb-4'>Lista de Usuarios</h2>
        <div
          className='max-h-[450px] overflow-y-scroll relative'
          style={{ scrollbarGutter: 'stable' }}
        >
          <table className='min-w-full bg-white shadow-md rounded mb-4'>
            <thead className='sticky top-0'>
              <tr>
                <th className='py-2 px-4 bg-gray-200 text-left'>Username</th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Rol</th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {users.map(user => (
                <tr key={user.id_user} className='border-b'>
                  <td className='py-2 px-4'>{user.username}</td>
                  <td className='py-2 px-4'>{user.rol}</td>
                  <td className='py-2 px-4 flex space-x-2'>
                    <button
                      onClick={() => handleDeleteUser(user.id_user)}
                      className='bg-red-300 hover:bg-red-500 text-white text-sm font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                    >
                      Eliminar
                    </button>

                    <button
                      onClick={() => {
                        setUserToEdit(user)
                      }}
                      className='bg-yellow-300 hover:bg-yellow-500 text-white text-sm font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
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
    </>
  )
}

export default UserForm
