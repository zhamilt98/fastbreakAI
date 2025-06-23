"use client";
import "../globals.css";
import { useContext, useState } from "react";
import AuthContext from "./auth_context";
import axios from "axios";

const Login = () => {
    const { login } = useContext(AuthContext);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [registerEmail, setRegisterEmail] = useState('');
    const [registerPassword, setRegisterPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        login(email, password)
    };

    const handleRegister = async (e) => {
      e.preventDefault();
      try {
        const response = await axios.post('http://localhost:8000/auth/signup', {
          email: registerEmail,
          password: registerPassword,
        });
        login(registerEmail, registerPassword);
      } catch(error) {
        console.error('Failed to register user:', error);
    }
  }

    return (
      <div className="container">
        <h2>Login</h2>
          <form onSubmit={handleSubmit}>
              <div className="form-group">
                  <label htmlFor="email" className="form-label">Email: </label>
              <input type="text" className="form-control" id="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
              </div>
              <div className="form-group">
                  <label htmlFor="password" className="form-label">Password: </label>
              <input type="password" className="form-control" id="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
              </div>
              <button type="submit">Login</button>
          </form>

      <h2>Sign Up</h2>
<form onSubmit={handleRegister}>
    <div className="form-group">
        <label htmlFor="registerEmail" className="form-label">Email: </label>
          <input
            type="text"
            className="form-control"
            id="registerEmail"
            value={registerEmail}
            onChange={(e) => setRegisterEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="registerPassword" className="form-label">Password: </label>
          <input
            type="password"
            className="form-control"
            id="registerPassword"
            value={registerPassword}
            onChange={(e) => setRegisterPassword(e.target.value)}
            required
          />
    </div>
    <button type="submit">Sign Up</button>
</form>
      </div>
      );

};

export default Login;