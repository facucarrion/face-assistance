import React, { useState, useEffect } from 'react';

const GroupsForm = () => {
    const [groups, setGroups] = useState([]);
    const [formData, setFormData] = useState({
        name: ''
    });
    const [editGroupId, setEditGroupId] = useState(null);

    const fetchGroups = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/groups/');
            const groupsData = await response.json();
            setGroups(groupsData);
        } catch (error) {
            console.error('Error al recuperar curso:', error);
        }
    };

    useEffect(() => {
        fetchGroups();
    }, []);

    const handleCreateOrUpdateGroup = async (event) => {
        event.preventDefault();

        try {
            const url = editGroupId 
                ? `http://127.0.0.1:8000/groups/${editGroupId}`
                : 'http://127.0.0.1:8000/groups/';
            const method = editGroupId ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                alert(editGroupId ? 'Curso actualizado exitosamente!' : 'Curso creado exitosamente!');
                fetchGroups();
                setFormData({ name: '' });
                setEditGroupId(null);
            } else {
                alert('No se pudo crear/actualizar el curso');
            }
        } catch (error) {
            console.error('Error al crear/actualizar curso:', error);
        }
    };

    const handleDeleteGroup = async (id_group) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/groups/${id_group}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                alert('¡Curso eliminado exitosamente!');
                fetchGroups();
            } else {
                alert('No se pudo eliminar el curso');
            }
        } catch (error) {
            console.error('Error al eliminar curso:', error);
        }
    };

    const handleChange = (event) => {
        setFormData({
            ...formData,
            [event.target.name]: event.target.value
        });
    };

    const handleEditGroup = (group) => {
        setFormData({ name: group.name });
        setEditGroupId(group.id_group);
    };

    return (
        <div className="max-w-md mx-auto">
            <h2 className="text-xl mb-2">{editGroupId ? 'Editar Curso' : 'Crear Curso'}</h2>
            <form onSubmit={handleCreateOrUpdateGroup} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <div className="mb-4">
                    <label htmlFor="name" className="block text-gray-700 text-sm font-bold mb-2">Nombre del Curso:</label>
                    <input type="text" id="name" name="name" placeholder="Ingrese el nombre del curso" required
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        value={formData.name} onChange={handleChange} />
                </div>
                <button type="submit"
                    className="bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                    {editGroupId ? 'Actualizar Curso' : 'Crear Curso'}
                </button>
            </form>

            <h2 className="text-xl mb-2">Lista de Cursos</h2>
            <table className="min-w-full bg-white shadow-md rounded">
                <thead>
                    <tr>
                        <th className="py-2">ID</th>
                        <th className="py-2">Nombre</th>
                        <th className="py-2">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {groups.map(group => (
                        <tr key={group.id_group}>
                            <td className="py-2">{group.id_group}</td>
                            <td className="py-2">{group.name}</td>
                            <td className="py-2">
                                <button onClick={() => handleDeleteGroup(group.id_group)}
                                    className="bg-red-300 hover:bg-red-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                                    Eliminar
                                </button>
                                <button onClick={() => handleEditGroup(group)}
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

export default GroupsForm;