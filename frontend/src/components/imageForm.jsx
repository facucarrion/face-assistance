import { useEffect, useState } from 'react'

const ImageForm = () => {
  const [people, setPeople] = useState([])
  const [isUploading, setIsUploading] = useState(false)
  const [tempImage, setTempImage] = useState(null)

  const fetchPeople = async () => {
    const response = await fetch('http://127.0.0.1:8000/people?limit=500')
    const peopleData = await response.json()

    setPeople(peopleData)
  }

  useEffect(() => {
    fetchPeople()
  }, [])

  useEffect(() => {
    console.log(people)
  }, [people])

  const handleUploadImage = async id_person => {
    const response = await fetch(
      `http://localhost:8000/temp_images/create_empty_temp_image`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id_person })
      }
    )
    if (!response.ok) {
      alert('No se ha podido poner la imagen en cola')
      return
    }
    const data = await response.json()
    setIsUploading(true)
    setTempImage(data)
  }

  const handleDeclineImage = async id_temp_images => {
    const response = await fetch(
      `http://localhost:8000/temp_images/${id_temp_images}`,
      {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
    const data = await response.json()
    console.log(data)
    setIsUploading(false)
    setTempImage(null)
  }

  return (
    <div className='grid grid-cols-2 gap-8'>
      <div className='w-full'>
        <h2 className='text-2xl font-bold mb-4'>Lista de Alumnos</h2>
        <div className='max-h-96 overflow-y-auto'>
          <table className='min-w-full bg-white shadow-md rounded mb-4'>
            <thead className='sticky top-0'>
              <tr>
                <th className='py-2 px-4 bg-gray-200 text-left'>Nombre</th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Apellido</th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Curso</th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Dispositivo</th>
                <th className='py-2 px-4 bg-gray-200 text-left'>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {people.map(person => (
                <tr key={person.id_person}>
                  <td className='py-2 px-4 border-b'>{person.firstname}</td>
                  <td className='py-2 px-4 border-b'>{person.lastname}</td>
                  <td className='py-2 px-4 border-b'>{person.group_name}</td>
                  <td className='py-2 px-4 border-b'>
                    {person.device_name ?? 'No asignado'}
                  </td>
                  <td className='py-2 px-4 border-b'>
                    {person.device_name && (
                      <button
                        onClick={() => handleUploadImage(person.id_person)}
                        className='bg-yellow-300 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                      >
                        Subir Imagen
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className='w-full'>
        <h2 className='text-2xl font-bold mb-4'>Previsualización</h2>
        <div className='w-full border-2 h-full'>
          {isUploading ? <p>Si</p> : <p>No</p>}
        </div>
        <div className='w-full grid grid-cols-2 gap-4'>
          <button
            className='py-2 border-2 bg-gray-500 text-white flex items-center justify-center'
            onClick={() => handleDeclineImage(tempImage.id_temp_images)}
          >
            Rechazar
          </button>
          <button className='py-2 border-2 bg-gray-500 text-white flex items-center justify-center'>
            Confirmar
          </button>
        </div>
      </div>
    </div>
  )
}

export default ImageForm
