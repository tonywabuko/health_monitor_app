import React, { useState } from 'react';
import { signup, login, getProtectedData } from './AuthService';

function AuthExample() {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: ''
    });
    const [isLogin, setIsLogin] = useState(true);
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [user, setUser] = useState(null);
    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            let response;
            if (isLogin) {
                response = await login({
                    email: formData.email,
                    password: formData.password
                });
            } else {
                response = await signup(formData);
            }
            
            setToken(response.token);
            setUser(response.user);
            localStorage.setItem('token', response.token);
            setMessage(response.message);
        } catch (err) {
            setMessage(err.message);
        }
    };

    const handleLogout = () => {
        setToken(null);
        setUser(null);
        localStorage.removeItem('token');
        setMessage('Logged out successfully');
    };

    const fetchProtectedData = async () => {
        try {
            const data = await getProtectedData(token);
            setMessage(data.message);
        } catch (err) {
            setMessage(err.message);
        }
    };

    return (
        <div>
            {!token ? (
                <div>
                    <h2>{isLogin ? 'Login' : 'Sign Up'}</h2>
                    <form onSubmit={handleSubmit}>
                        {!isLogin && (
                            <div>
                                <label>Username</label>
                                <input
                                    type="text"
                                    name="username"
                                    value={formData.username}
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                        )}
                        <div>
                            <label>Email</label>
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div>
                            <label>Password</label>
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                required
                                minLength="6"
                            />
                        </div>
                        <button type="submit">{isLogin ? 'Login' : 'Sign Up'}</button>
                    </form>
                    <button onClick={() => setIsLogin(!isLogin)}>
                        {isLogin ? 'Need an account? Sign Up' : 'Already have an account? Login'}
                    </button>
                </div>
            ) : (
                <div>
                    <h2>Welcome, {user?.username}!</h2>
                    <p>Email: {user?.email}</p>
                    <button onClick={fetchProtectedData}>Get Protected Data</button>
                    <button onClick={handleLogout}>Logout</button>
                </div>
            )}
            {message && <p>{message}</p>}
        </div>
    );
}

export default AuthExample;