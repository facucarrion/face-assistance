import React, { useState, useEffect } from 'react'

const GroupsForm = () => {
  const [groups, setGroups] = useState([])
  const [formData, setFormData] = useState({
    name: ''
  })
  const [editGroupId, setEditGroupId] = useState(null)

  const fetchGroups = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/groups/')
      const groupsData = await response.json()
      setGroups(groupsData)
    } catch (error) {
      console.error('Error al recuperar curso:', error)
    }
  }

  useEffect(() => {
    fetchGroups()
  }, [])

  const handleCreateOrUpdateGroup = async event => {
    event.preventDefault()

    try {
      const url = editGroupId
        ? `http://127.0.0.1:8000/groups/${editGroupId}`
        : 'http://127.0.0.1:8000/groups/'
      const method = editGroupId ? 'PUT' : 'POST'

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        alert(
          editGroupId
            ? 'Curso actualizado exitosamente!'
            : 'Curso creado exitosamente!'
        )
        fetchGroups()
        setFormData({ name: '' })
        setEditGroupId(null)
      } else {
        alert('No se pudo crear/actualizar el curso')
      }
    } catch (error) {
      console.error('Error al crear/actualizar curso:', error)
    }
  }

  const handleDeleteGroup = async id_group => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/groups/${id_group}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        alert('¡Curso eliminado exitosamente!')
        fetchGroups()
      } else {
        alert('No se pudo eliminar el curso')
      }
    } catch (error) {
      console.error('Error al eliminar curso:', error)
    }
  }

  const handleChange = event => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value
    })
  }

  const handleEditGroup = group => {
    setFormData({ name: group.name })
    setEditGroupId(group.id_group)
  }

  return (
    <>
      <div className='w-full'>
        <h2 className='text-2xl font-bold mb-4'>
          {editGroupId ? 'Editar Curso' : 'Crear Curso'}
        </h2>
        <form
          onSubmit={handleCreateOrUpdateGroup}
          className='bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 flex flex-col justify-between'
        >
          <div className='mb-4'>
            <label
              htmlFor='name'
              className='block text-gray-700 text-sm font-bold mb-2'
            >
              Nombre del Curso:
            </label>
            <input
              className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
              type='text'
              name='name'
              id='name'
              placeholder='Ingrese el nombre del curso'
              required
              value={formData.name}
              onChange={handleChange}
            />
          </div>

          <div className='w-full grid grid-cols-2'>
            <button
              type='submit'
              className='bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
            >
              {editGroupId ? 'Actualizar Curso' : 'Crear Curso'}
            </button>
            {editGroupId && (
              <button
                type='button'
                className='bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                onClick={() => {
                  setEditGroupId(null)
                  setFormData({
                    name: ''
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
        <h2 className='text-2xl font-bold mb-4'>Lista de Cursos</h2>
        <div className='max-h-96 overflow-y-auto'>
          <table className='min-w-full bg-white shadow-md rounded mb-4'>
            <thead>
              <tr>
                <th className='py-2 px-4 bg-gray-200 text-left'>Nombre</th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {groups.map(group => (
                <tr key={group.id_group}>
                  <td className='py-2 px-4 border-b'>{group.name}</td>
                  <td className='py-2 px-4 border-b'>
                    <button
                      onClick={() => handleDeleteGroup(group.id_group)}
                      className='bg-red-300 hover:bg-red-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                    >
                      Eliminar
                    </button>

                    <button
                      onClick={() => handleEditGroup(group)}
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
    </>
  )
}

export default GroupsForm
