import { useState, useEffect } from 'react'

const SchedulesForm = () => {
  const [groups, setGroups] = useState([])
  const [schedules, setSchedules] = useState([])
  const [selectedGroup, setSelectedGroup] = useState('')
  const [days, setDays] = useState([])
  const [newSchedule, setNewSchedule] = useState({
    id_day: '',
    start_time: '',
    end_time: ''
  })

  useEffect(() => {
    fetchGroups()
    fetchDays()
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

  const fetchDays = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/days/')
      if (response.ok) {
        const daysData = await response.json()
        setDays(daysData)
      } else {
        console.error('Error al recuperar días:', response.statusText)
      }
    } catch (error) {
      console.error('Error al recuperar días:', error)
    }
  }

  const fetchSchedules = async id_group => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/schedules/${id_group}`
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

  const handleDelete = async id_schedule => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/schedules/${id_schedule}`, {
        method: 'DELETE'
      })
      if (response.ok) {
        fetchSchedules(selectedGroup)
        console.log('Horario eliminado')
      } else {
        console.error('Error al eliminar horario:', response.statusText)
      }
    } catch (error) {
      console.error('Error al eliminar horario:', error)
    }
  }

  return (
    <div className='w-full'>
      <h2 className='text-2xl font-bold mb-4'>Gestionar Horarios</h2>
      <div className="flex space-x-8"> 
        <div className='w-1/2'> 
          <div className='mb-4'>
            <label
              htmlFor='id_group'
              className="block text-gray-700 text-sm font-bold mb-2"
            >
              Seleccionar Curso:
            </label>
            <select
              className="block w-full bg-gray-100 border border-gray-300 rounded py-2 px-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
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

          <form onSubmit={handleSubmit} className='bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4'>
            <h3 className='text-lg font-bold mb-2'>Agregar Nuevo Horario</h3>
            <label htmlFor="day" className='block text-gray-700 text-sm font-bold mb-2'>
              Día de la semana:
            </label>
            <select
              id="day"
              name="id_day"
              value={newSchedule.id_day}
              onChange={handleInputChange}
              className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
            >
              <option value="">Selecciona un día</option>
              {days.map((day) => (
                <option key={day.id_day} value={day.id_day}>
                  {day.day}
                </option>
              ))}
            </select>

            <div className='mb-4'>
              <label htmlFor='start_time' className='block text-gray-700 text-sm font-bold mb-2'>
                Hora de inicio:
              </label>
              <input
                type='time'
                id='start_time'
                name='start_time'
                value={newSchedule.start_time}
                onChange={handleInputChange}
                className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
                required
              />
            </div>

            <div className='mb-4'>
              <label htmlFor='end_time' className='block text-gray-700 text-sm font-bold mb-2'>
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
              className='bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
            >
              Agregar Horario
            </button>
          </form>
        </div>
        <div className='w-1/2'> 
          {selectedGroup && (
            <div>
              <h3 className='text-lg font-bold mb-2'>Horarios del Curso</h3>
              <div className='grid grid-cols-1 gap-4'>
                {schedules.length > 0 ? (
                  schedules.map(schedule => (
                    <div key={schedule.id_schedule} className='border p-4 rounded shadow-md'>
                      <p><strong>Día:</strong> {schedule.id_day}</p>
                      <p><strong>Horario:</strong> {schedule.start_time} - {schedule.end_time}</p>
                    </div>
                  ))
                ) : (
                  <p>No hay horarios disponibles para este curso.</p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default SchedulesForm