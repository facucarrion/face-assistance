import { useState, useEffect } from 'react'

const DeviceForm = () => {
  const [devices, setDevices] = useState([])
  const [states, setStates] = useState([])
  const [editDeviceId, setEditDeviceId] = useState(null)
  const [formData, setFormData] = useState({
    id_config: '',
    name: '',
    id_state: 1
  })

  const fetchDevices = async () => {
    const response = await fetch('http://localhost:8000/devices')
    const devicesData = await response.json()
    setDevices(devicesData)
  }

  useEffect(() => {
    console.log(formData)
  }, [formData])

  useEffect(() => {
    const fetchStates = async () => {
      const response = await fetch('http://localhost:8000/states')
      const statesData = await response.json()
      setStates(statesData)
    }

    fetchDevices()
    fetchStates()
  }, [])

  const handleChange = event => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value
    })
  }

  const handleCreateOrUpdateDevice = async event => {
    event.preventDefault()

    const url = editDeviceId
      ? `http://127.0.0.1:8000/devices/${editDeviceId}`
      : 'http://127.0.0.1:8000/devices/'

    const method = editDeviceId ? 'PUT' : 'POST'

    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })

    if (response.ok) {
      alert(
        editDeviceId
          ? 'Dispositivo actualizado exitosamente!'
          : 'Dispositivo creado exitosamente!'
      )
      setFormData({ id_config: '', name: '', id_state: 1 })
      setEditDeviceId(null)
      fetchDevices()
    }

    if (!response.ok) {
      alert('No se pudo crear/actualizar el dispositivo')
    }
  }

  const handleEditDevice = device => {
    console.log (device)
    setFormData({
      id_config: device.id_config,
      name: device.name,
      id_state: device.id_state
    })
    setEditDeviceId(device.id_device)
  }

  const handleDeleteDevice = async id_device => {
    const response = await fetch(`http://127.0.0.1:8000/devices/${id_device}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      alert('¡Dispositivo eliminado exitosamente!')
      fetchDevices()
    } else {
      alert('No se pudo eliminar el dispositivo')
    }
  }

  return (
    <div className='grid grid-cols-2 gap-8'>
      <div className='w-full'>
        <h2 className='text-2xl font-bold mb-4'>
          {editDeviceId ? 'Editar Dispositivo' : 'Crear Dispositivo'}
        </h2>
        <form
          onSubmit={handleCreateOrUpdateDevice}
          className='bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 flex flex-col justify-between'
        >
          <div className='mb-4'>
            <label
              htmlFor='id_config'
              className='block text-gray-700 text-sm font-bold mb-2'
            >
              ID del Dispositivo:
            </label>
            <input
              className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
              type='text'
              name='id_config'
              id='id_config'
              placeholder='Ingrese el id del dispositivo'
              required
              value={formData.id_config}
              onChange={handleChange}
            />
          </div>

          <div className='mb-4'>
            <label
              htmlFor='name'
              className='block text-gray-700 text-sm font-bold mb-2'
            >
              Nombre del Dispositivo:
            </label>
            <input
              className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
              type='text'
              name='name'
              id='name'
              placeholder='Ingrese el nombre del dispositivo'
              required
              value={formData.name}
              onChange={handleChange}
            />
          </div>

          <div className='mb-4'>
            <label
              htmlFor='id_state'
              className='block text-gray-700 text-sm font-bold mb-2'
            >
              Estado:
            </label>
            <select
              className='shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
              name='id_state'
              id='id_state'
              value={formData.id_state}
              onChange={handleChange}
              required
            >
              {states.map(state => (
                <option key={state.id_state} value={state.id_state} checked={formData.id_state == state.id_state}>
                  {state.state}
                </option>
              ))}
            </select>
          </div>

          <div className='w-full grid grid-cols-2'>
            <button
              type='submit'
              className='bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
            >
              {editDeviceId ? 'Actualizar Dispositivo' : 'Crear Dispositivo'}
            </button>
            {editDeviceId && (
              <button
                type='button'
                className='bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                onClick={() => {
                  setEditDeviceId(null)
                  setFormData({
                    id_config: '',
                    name: '',
                    id_state: 1
                  })
                }}
              >
                Limpiar
              </button>
            )}
          </div>
        </form>
      </div>

      <div>
        <h2 className='text-lg font-bold mb-2'>Lista de Dispositivos</h2>
        <div className='max-h-96 overflow-y-auto relative'>
          <table className='min-w-full bg-white shadow-md rounded mb-4'>
            <thead className='sticky top-0'>
              <tr>
                <th className='py-2 px-4 bg-gray-200 text-left'>
                  Id del Dispositivo
                </th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Nombre</th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Estado</th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {devices.map(device => (
                <tr key={device.id_device}>
                  <td className='py-2 px-4 border-b'>{device.id_config}</td>
                  <td className='py-2 px-4 border-b'>{device.name}</td>
                  <td className='py-2 px-4 border-b'>{device.state}</td>
                  <td className='py-2 px-4 border-b'>
                    <button
                      onClick={() => handleDeleteDevice(device.id_device)}
                      className='bg-red-300 hover:bg-red-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                    >
                      Eliminar
                    </button>

                    <button
                      onClick={() => handleEditDevice(device)}
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

export default DeviceForm
