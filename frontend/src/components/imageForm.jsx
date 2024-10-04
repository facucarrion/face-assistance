import { useEffect, useState } from 'react'

const ImageForm = () => {
  const [people, setPeople] = useState([])

  const fetchPeople = async () => {
    const response = await fetch('http://127.0.0.1:8000/people?limit=500')
    const peopleData = await response.json()

    setPeople(peopleData)
  }

  useEffect(() => {
    fetchPeople()
  }, [])

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
                <th className='py-2 px-4 bg-gray-200 text-left'>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {people.map(people => (
                <tr key={people.id_person}>
                  <td className='py-2 px-4 border-b'>{people.firstname}</td>
                  <td className='py-2 px-4 border-b'>{people.lastname}</td>
                  <td className='py-2 px-4 border-b'>
                    <button
                      onClick={() => handleEditPeople(people)}
                      className='bg-yellow-300 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline'
                    >
                      Subir Imagen
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className='w-full'></div>
    </div>
  )
}

export default ImageForm
