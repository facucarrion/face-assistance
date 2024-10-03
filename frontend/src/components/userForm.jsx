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
  const [userPermissions, setUserPermissions] = useState(null)
  const [roles, setRoles] = useState([])
  const [groups, setGroups] = useState([])
  const [selectedGroups, setSelectedGroups] = useState([])

  const fetchUsers = async () => {
    const response = await fetch('http://127.0.0.1:8000/users/')
    const usersData = await response.json()
    setUsers(usersData)
  }

  const fetchRoles = async () => {
    const response = await fetch('http://127.0.0.1:8000/users/roles/')
    const rolesData = await response.json()
    setRoles(rolesData)
  }

  const fetchGroups = async () => {
    const response = await fetch('http://127.0.0.1:8000/groups/')
    const groupsData = await response.json()

    setGroups(groupsData)

    if (groupsData.length > 0) {
      setFormData(prevFormData => ({
        ...prevFormData,
        id_group: groupsData[0].id_group
      }))
    }
  }

  useEffect(() => {
    fetchUsers()
    fetchRoles()
    fetchGroups()
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
  }

  const handleDeleteUser = async id_user => {
    const response = await fetch(`http://127.0.0.1:8000/users/${id_user}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      alert('¡Usuario eliminado exitosamente!')
      fetchUsers()
    } else {
      alert('No se pudo eliminar el usuario')
    }
  }

  const handleUpdateUser = async event => {
    event.preventDefault()

    if (formData.password && formData.password !== formData.repeat_password) {
      alert('Las contraseñas no coinciden')
      return
    }

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
  }

  const handleChange = event => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value
    })
  }

  useEffect(() => {
    if (userPermissions) {
      fetchUserPermissions(userPermissions.id_user)
    }
  }, [userPermissions])

  const fetchUserPermissions = async (id_user) => {
    const response = await fetch(`http://127.0.0.1:8000/users/${id_user}/permissions`)
    if (!response.ok) {
      throw new Error('Error al obtener los permisos del usuario')
    }
    const permissionsData = await response.json()
    const userGroupsIds = permissionsData.map(permission => permission.id_group) // Cambiar a id_group
    setSelectedGroups(userGroupsIds)
  }

  const handleGroupsChange = (event) => {
    const groupsId = parseInt(event.target.value)
    if (event.target.checked) {
      setSelectedGroups([...selectedGroups, groupsId])
    } else {
      setSelectedGroups(selectedGroups.filter(id => id !== groupsId))
    }
  }

  // Manejador para guardar permisos
  const handleSavePermissions = async (event) => {
    event.preventDefault()

    const response = await fetch(`http://127.0.0.1:8000/users/${userPermissions.id_user}/permissions/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ groups: selectedGroups })
    })

    if (response.ok) {
      alert('Permisos actualizados exitosamente!')
      setUserPermissions(null)
      setSelectedGroups([])
    } else {
      const errorData = await response.json()
      alert(`No se pudo actualizar los permisos: ${errorData.detail || 'Error desconocido'}`)
    }
  }

  return (
    <>
      <div className='w-full'>
        <h2 className='text-2xl font-bold mb-4'>
          {!userPermissions ? (userToEdit ? 'Editar Usuario' : 'Crear Usuario') : `Permisos para ${userPermissions.username}`}
        </h2>
        {!userPermissions ? (
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
        ) : (
          // Formulario de Permisos
          <form onSubmit={handleSavePermissions} className='bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4'>
            <div className='mb-6'>
              {groups.length > 0 ? (
                groups.map(group => (
                  <div key={group.id_group} className='flex items-center mb-3'>
                    <input
                      type='checkbox'
                      id={`group-${group.id_group}`}
                      name='groups'
                      value={group.id_group}
                      checked={selectedGroups.includes(group.id_group)}
                      onChange={handleGroupsChange}
                      className="mr-3 h-5 w-5 accent-blue-400 border-gray-300 rounded"
                    />
                    <label htmlFor={`group-${group.id_group}`} className='text-gray-700'>
                      {group.name}
                    </label>
                  </div>
                ))
              ) : (
                <p className="text-gray-600">No hay cursos disponibles.</p>
              )}
            </div>
            <div className='grid grid-cols-2 gap-4'>
              <button
                type='submit'
                className='bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
              >
                Guardar Permisos
              </button>
              <button
                type='button'
                className='bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                onClick={() => setUserPermissions(null)}
              >
                Cancelar
              </button>
            </div>
          </form>
        )}
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

                    {user.id_rol !== 1 && (
                      <button
                        onClick={() => {
                          setUserPermissions(user);
                          fetchUserPermissions(user.id_user);
                        }}
                        className='bg-green-300 hover:bg-green-500 text-white text-sm font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                      >
                        Permisos
                      </button>
                    )}
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
