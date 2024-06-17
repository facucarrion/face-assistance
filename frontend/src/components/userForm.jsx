import React, { useState, useEffect } from 'react';

const UserForm = () => {
    const [users, setUsers] = useState([]);
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        id_rol: 0
    });

    const fetchUsers = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/auth/');
            const usersData = await response.json();
            setUsers(usersData);
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    const handleCreateUser = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch('http://127.0.0.1:8000/auth/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                alert('User created successfully!');
                fetchUsers();
            } else {
                alert('Failed to create user');
            }
        } catch (error) {
            console.error('Error creating user:', error);
        }
    };

    const handleDeleteUser = async (id_user) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/auth/${id_user}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                alert('User deleted successfully!');
                fetchUsers();
            } else {
                alert('Failed to delete user');
            }
        } catch (error) {
            console.error('Error deleting user:', error);
        }
    };

    const handleChange = (event) => {
        setFormData({
            ...formData,
            [event.target.name]: event.target.value
        });
    };

    return (
        <div className="max-w-md mx-auto">
            <h2 className="text-xl mb-2">Crear Usuario</h2>
            <form onSubmit={handleCreateUser} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <div className="mb-4">
                    <label htmlFor="username" className="block text-gray-700 text-sm font-bold mb-2">Nombre de Usuario:</label>
                    <input type="text" id="username" name="username" placeholder="Ingrese el nombre de usuario" required
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        value={formData.username} onChange={handleChange} />
                </div>
                <div className="mb-4">
                    <label htmlFor="password" className="block text-gray-700 text-sm font-bold mb-2">Contraseña:</label>
                    <input type="password" id="password" name="password" placeholder="Ingrese la contraseña" required
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        value={formData.password} onChange={handleChange} />
                </div>
                <div className="mb-4">
                    <label htmlFor="id_rol" className="block text-gray-700 text-sm font-bold mb-2">Rol:</label>
                    <input type="number" id="id_rol" name="id_rol" placeholder="Ingrese el rol" required
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        value={formData.id_rol} onChange={handleChange} />
                </div>
                <button type="submit"
                    className="bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                    Crear Usuario
                </button>
            </form>

            <h2 className="text-xl mb-2">Lista de Usuarios</h2>
            <table className="min-w-full bg-white shadow-md rounded">
                <thead>
                    <tr>
                        <th className="py-2">ID</th>
                        <th className="py-2">Username</th>
                        <th className="py-2">Rol</th>
                        <th className="py-2">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map(user => (
                        <tr key={user.id_user}>
                            <td className="py-2">{user.id_user}</td>
                            <td className="py-2">{user.username}</td>
                            <td className="py-2">{user.rol}</td>
                            <td className="py-2">
                                <button onClick={() => handleDeleteUser(user.id_user)}
                                    className="bg-red-300 hover:bg-red-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                                    Eliminar
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default UserForm;
