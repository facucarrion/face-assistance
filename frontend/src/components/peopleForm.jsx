import React, { useState, useEffect } from 'react';

const PeopleForm = () => {
    const [people, setPeople] = useState([]);
    const [formData, setFormData] = useState({
        firstname: '',
        lastname: '',
        document: '',
        image: '',
        id_group: 0
    });
    const [editPeopleId, setEditPeopleId] = useState(null);

    const fetchPeople = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/people/');
            const peopleData = await response.json();
            setPeople(peopleData);
        } catch (error) {
            console.error('Error al recuperar alumno:', error);
        }
    };

    useEffect(() => {
        fetchPeople();
    }, []);

    const handleCreateOrUpdatePeople = async (event) => {
        event.preventDefault();

        try {
            const url = editPeopleId 
                ? `http://127.0.0.1:8000/people/${editPeopleId}`
                : 'http://127.0.0.1:8000/people/';
            const method = editPeopleId ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                alert(editPeopleId ? 'Alumno actualizado exitosamente!' : 'Alumno creado exitosamente!');
                fetchPeople();
                setFormData({
                    firstname: '',
                    lastname: '',
                    document: '',
                    image: '',
                    id_group: 0
                });
                setEditPeopleId(null);
            } else {
                alert('No se pudo crear/actualizar el alumno');
            }
        } catch (error) {
            console.error('Error al crear/actualizar alumno:', error);
        }
    };

    const handleDeletePeople = async (id_person) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/people/${id_person}`, {
                method: 'DELETE',
            });
    
            if (response.ok) {
                alert('¡Alumno eliminado exitosamente!');
                fetchPeople();
            } else {
                alert('No se pudo eliminar el alumno');
            }
        } catch (error) {
            console.error('Error al eliminar alumno:', error);
        }
    };

    const handleChange = (event) => {
        setFormData({
            ...formData,
            [event.target.name]: event.target.value
        });
    };

    const handleEditPeople = (people) => {
        setFormData({
            firstname: people.firstname,
            lastname: people.lastname,
            document: people.document,
            image: people.image,
            id_group: people.id_group
        });
        setEditPeopleId(people.id_person);
    };

    return (
        <div className="max-w-md mx-auto mt-10">
            <h2 className="text-2xl font-bold mb-4">{editPeopleId ? 'Editar Alumno' : 'Crear Alumno'}</h2>
            <form onSubmit={handleCreateOrUpdatePeople} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <div className="mb-4">
                    <label htmlFor="firstname" 
                    className="block text-gray-700 text-sm font-bold mb-2">
                    Nombre:
                    </label>
                    <input 
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    type="text"
                    name="firstname"
                    id="firstname" 
                    placeholder="Ingrese el nombre del alumno" required
                    value={formData.firstname} onChange={handleChange} 
                    />
                </div>

                <div className="mb-4">
                    <label htmlFor="lastname" 
                    className="block text-gray-700 text-sm font-bold mb-2">
                    Apellido:
                    </label>
                    <input
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    type="text" 
                    name="lastname"
                    id="lastname" 
                    placeholder="Ingrese el apellido del alumno" required
                    value={formData.lastname} onChange={handleChange} 
                    />
                </div>

                <div className="mb-4">
                    <label htmlFor="document" 
                    className="block text-gray-700 text-sm font-bold mb-2">
                    Documento:
                    </label>
                    <input 
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    type="text"
                    name="document"
                    id="document" 
                    placeholder="Ingrese el documento del alumno" required
                    value={formData.document} onChange={handleChange} 
                    />
                </div>

                <div className="mb-4">
                    <label htmlFor="image" 
                    className="block text-gray-700 text-sm font-bold mb-2">
                    Imagen:
                    </label>
                    <input
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    type="text"
                    name="image"
                    id="image" 
                    placeholder="Ingrese la URL de la imagen del alumno" required
                    value={formData.image} onChange={handleChange} 
                    />
                </div>

                <div className="mb-4">
                    <label htmlFor="id_group" 
                    className="block text-gray-700 text-sm font-bold mb-2">
                    Grupo:
                    </label>
                    <input
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    type="number"
                    name="id_group" 
                    id="id_group"
                    placeholder="Ingrese el ID del grupo" required
                    value={formData.id_group} onChange={handleChange} 
                    />
                </div>

                <button type="submit"
                    className="bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                    {editPeopleId ? 'Actualizar Alumno' : 'Crear Alumno'}
                </button>
            </form>

            <h2 className="text-2xl font-bold mb-4">Lista de Alumnos</h2>
            <table className="min-w-full bg-white shadow-md rounded mb-4">
                <thead>
                    <tr>
                        <th className="py-2 px-4 bg-gray-200 text-left">Nombre</th>
                        <th className="py-2 px-4 bg-gray-200 text-left">Apellido</th>
                        <th className="py-2 px-4 bg-gray-200 text-left">Documento</th>
                        <th className="py-2 px-4 bg-gray-200 text-left">Acciones</th>
                    </tr>
                </thead>

                <tbody>
                    {people.map(people => (
                        <tr key={people.id_person}>
                            
                            <td className="py-2 px-4 border-b">{people.firstname}</td>
                            <td className="py-2 px-4 border-b">{people.lastname}</td>
                            <td className="py-2 px-4 border-b">{people.document}</td>
                            <td className="py-2 px-4 border-b">

                                <button onClick={() => handleDeletePeople(people.id_person)}
                                    className="bg-red-300 hover:bg-red-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                                    Eliminar
                                </button>
                                
                                <button onClick={() => handleEditPeople(people)}
                                    className="bg-yellow-300 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                                    Editar
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default PeopleForm;