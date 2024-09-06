import { useState, useEffect } from 'react'

const SchedulesForm = () => {
  const [groups, setGroups] = useState([])
  const [schedules, setSchedules] = useState([])
  const [selectedGroup, setSelectedGroup] = useState('')
  const [newSchedule, setNewSchedule] = useState({
    id_day: '',
    start_time: '',
    end_time: ''
  })

  useEffect(() => {
    fetchGroups()
  }, [])

  useEffect(() => {
    if (selectedGroup) {
      fetchSchedules(selectedGroup)
    }
  }, [selectedGroup])

  const fetchGroups = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/groups/')
      if (response.ok) {
        const groupsData = await response.json()
        setGroups(groupsData)
        if (groupsData.length > 0) {
          setSelectedGroup(groupsData[0].id_group)
        }
      } else {
        console.error('Error al recuperar grupos:', response.statusText)
      }
    } catch (error) {
      console.error('Error al recuperar grupos:', error)
    }
  }

  const fetchSchedules = async id_group => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/schedules?id_group=${id_group}`
      )
      if (response.ok) {
        const schedulesData = await response.json()
        setSchedules(schedulesData)
      } else {
        console.error('Error al recuperar horarios:', response.statusText)
      }
    } catch (error) {
      console.error('Error al recuperar horarios:', error)
    }
  }

  const handleGroupChange = event => {
    setSelectedGroup(event.target.value)
  }

  const handleInputChange = event => {
    const { name, value } = event.target
    setNewSchedule({
      ...newSchedule,
      [name]: value
    })
  }

  const handleSubmit = async event => {
    event.preventDefault()
    try {
      const response = await fetch('http://127.0.0.1:8000/schedules', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id_group: selectedGroup,
          ...newSchedule
        })
      })
      if (response.ok) {
        setNewSchedule({
          id_day: '',
          start_time: '',
          end_time: ''
        })
        fetchSchedules(selectedGroup)
        console.log(await response.json())
      } else {
        console.error('Error al crear horario:', response.statusText)
      }
    } catch (error) {
      console.error('Error al crear horario:', error)
    }
  }

  return (
    <div className='w-full'>
      <h2 className='text-2xl font-bold mb-4'>Horarios de Cursos</h2>

      <div className='mb-4'>
        <label
          htmlFor='id_group'
          className='block text-gray-700 text-sm font-bold mb-2'
        >
          Curso:
        </label>
        <select
          className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
          name='id_group'
          id='id_group'
          value={selectedGroup}
          onChange={handleGroupChange}
          required
        >
          {groups.map(group => (
            <option key={group.id_group} value={group.id_group}>
              {group.name}
            </option>
          ))}
        </select>
      </div>

      {selectedGroup && (
        <div className='mb-4'>
          <h3 className='text-lg font-bold mb-2'>Horarios del Curso</h3>
          {schedules.length > 0 ? (
            <ul className='list-disc pl-5'>
              {schedules.map(schedule => (
                <li key={schedule.id_schedule}>
                  {`Día ${schedule.id_day}: ${schedule.start_time} - ${schedule.end_time}`}
                </li>
              ))}
            </ul>
          ) : (
            <p>No hay horarios disponibles para este curso.</p>
          )}
        </div>
      )}

      <form onSubmit={handleSubmit} className='mt-6'>
        <h3 className='text-lg font-bold mb-2'>Agregar Nuevo Horario</h3>
        <div className='mb-4'>
          <label
            htmlFor='id_day'
            className='block text-gray-700 text-sm font-bold mb-2'
          >
            Día:
          </label>
          <input
            type='number'
            id='id_day'
            name='id_day'
            value={newSchedule.id_day}
            onChange={handleInputChange}
            className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
            required
          />
        </div>
        <div className='mb-4'>
          <label
            htmlFor='start_time'
            className='block text-gray-700 text-sm font-bold mb-2'
          >
            Hora de inicio:
          </label>
          <input
            type='time'
            id='start_time'
            name='start_time'
            value={newSchedule.start_time}
            onChange={handleInputChange}
            className='shadow appearance-none border rounded w-full py-2 px-3 text
            gray-700 leading-tight focus:outline-none focus:shadow-outline'
            required
          />
        </div>
        <div className='mb-4'>
          <label
            htmlFor='end_time'
            className='block text-gray-700 text-sm font-bold mb-2'
          >
            Hora de fin:
          </label>
          <input
            type='time'
            id='end_time'
            name='end_time'
            value={newSchedule.end_time}
            onChange={handleInputChange}
            className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
            required
          />
        </div>
        <button
          type='submit'
          className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
        >
          Agregar Horario
        </button>
      </form>
    </div>
  )
}

export default SchedulesForm