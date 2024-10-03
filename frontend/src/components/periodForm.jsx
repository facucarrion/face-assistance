import { useState, useEffect } from 'react'

const PeriodForm = () => {
  const [periods, setPeriods] = useState([])
  const [newPeriods, setNewPeriods] = useState({
    start_date: '',
    end_date: '',
    vacation_start: '',
    vacation_end: '',
    year: ''
  })
  const [editPeriodsId, setEditPeriodsId] = useState(null)

  const handleCreateOrUpdatePeriods = async event => {
    event.preventDefault()

    const url = editPeriodsId
      ? `http://127.0.0.1:8000/periods/${editPeriodsId}`
      : 'http://127.0.0.1:8000/periods/'
    const method = editPeriodsId ? 'PUT' : 'POST'

    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newPeriods)
    })

    if (response.ok) {
      alert(
        editPeriodsId
          ? 'Ciclo lectivo actualizado exitosamente!'
          : 'Ciclo lectivo exitosamente!'
      )

      setNewPeriods({
        start_date: '',
        end_date: '',
        vacation_start: '',
        vacation_end: '',
        year: ''
      })
      setEditPeriodsId(null)
    } else {
      alert('No se pudo crear/actualizar el ciclo lectivo')
    }
  }

  const handleDeletePeriods = async id_period => {
    const response = await fetch(`http://127.0.0.1:8000/periods/${id_period}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      alert('¡Ciclo lectivo eliminado exitosamente!')
    } else {
      alert('No se pudo eliminar el ciclo lectivo')
    }
  }

  const handleChange = event => {
    setNewPeriods({
      ...newPeriods,
      [event.target.name]: event.target.value
    })
  }

  return (
    <>
      <div className='w-full'>
        <h2 className='text-2xl font-bold mb-4'>
          {editPeriodsId ? 'Editar Ciclo Lectivo' : 'Crear Ciclo Lectivo'}
        </h2>
        <form
          onSubmit={handleCreateOrUpdatePeriods}
          className='bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 flex flex-col justify-between'
        >
          <div className='mb-4'>
            <label
              htmlFor='start_date'
              className='block text-gray-700 text-sm font-bold mb-2'
            >
              Fecha de Inicio:
            </label>
            <input
              type='date'
              id='start_date'
              name='start_date'
              value={newPeriods.start_date}
              onChange={handleChange}
              className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
              required
            />
          </div>

          <div className='mb-4'>
            <label
              htmlFor='end_date'
              className='block text-gray-700 text-sm font-bold mb-2'
            >
              Fecha de Finalización:
            </label>
            <input
              type='date'
              id='end_date'
              name='end_date'
              value={newPeriods.end_date}
              onChange={handleChange}
              className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
              required
            />
          </div>

          <div className='mb-4'>
            <label
              htmlFor='vacation_start'
              className='block text-gray-700 text-sm font-bold mb-2'
            >
              Inicio de Vacaciones:
            </label>
            <input
              type='date'
              id='vacation_start'
              name='vacation_start'
              value={newPeriods.vacation_start}
              onChange={handleChange}
              className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
              required
            />
          </div>

          <div className='mb-4'>
            <label
              htmlFor='vacation_end'
              className='block text-gray-700 text-sm font-bold mb-2'
            >
              Finalización de Vacaciones:
            </label>
            <input
              type='date'
              id='vacation_end'
              name='vacation_end'
              value={newPeriods.vacation_end}
              onChange={handleChange}
              className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
              required
            />
          </div>

          <div className='mb-4'>
            <label
              htmlFor='year'
              className='block text-gray-700 text-sm font-bold mb-2'
            >
              Ciclo Lectivo:
            </label>
            <input
              type='text'
              id='year'
              name='year'
              value={newPeriods.year}
              onChange={handleChange}
              className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
              required
            />
          </div>

          <div className='w-full grid grid-cols-2'>
            <button
              type='submit'
              className='bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
            >
              {editPeriodsId ? 'Actualizar Ciclo Lectivo' : 'Crear Ciclo Lectivo'}
            </button>
            {editPeriodsId && (
              <button
                type='button'
                className='bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                onClick={() => {
                  setEditPeriodsId(null)
                  setNewPeriods({
                    start_date: '',
                    end_date: '',
                    vacation_start: '',
                    vacation_end: '',
                    year: ''
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
        <div className='max-h-96 overflow-y-auto relative'>
          <table className='min-w-full bg-white shadow-md rounded mb-4'>
            <thead className='sticky top-0'>
              <tr>
                <th className='py-2 px-4 bg-gray-200 text-left'>Nombre</th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {/* {groups.map(group => (
                <tr key={group.id_group}>
                  {/* <td className='py-2 px-4 border-b'>{group.name}</td> */}
                  {/* <td className='py-2 px-4 border-b'> */} 
                    {/* <button
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
              ))} */}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}

export default PeriodForm
