import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const LoginPage = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleGoogleLogin = async () => {
    const response = await axios.get('/api/trigger-events-caller');
    console.log('Google login clicked');
    console.log(response);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
  };

  return (
    <div className="min-h-screen bg-[#0D1821] flex flex-col items-center justify-center p-4">
  <div className="text-2xl text-white font-bold mb-6">Routine Radar</div>

  <div className="max-w-md w-full bg-[#1A2631] rounded-xl shadow-lg p-8">
    <h2 className="text-2xl font-bold text-[#5CC8FF] mb-6">🔑 Login</h2>

    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-gray-400 mb-1">Email Address</label>
        <input
          type="email"
          required
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          className="w-full p-3 rounded-lg bg-[#0D1821] text-white border border-gray-600 focus:border-[#5CC8FF] focus:ring-2 focus:ring-[#5CC8FF]"
        />
      </div>

      <div>
        <label className="block text-gray-400 mb-1">Password</label>
        <div className="relative">
          <input
            type={showPassword ? 'text' : 'password'}
            required
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            className="w-full p-3 rounded-lg bg-[#0D1821] text-white border border-gray-600 focus:border-[#5CC8FF] focus:ring-2 focus:ring-[#5CC8FF]"
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute inset-y-0 right-3 flex items-center text-gray-400 hover:text-[#5CC8FF]"
          >
            {showPassword ? '🙈' : '👁️'}
          </button>
        </div>
      </div>

      <button
        onClick={handleGoogleLogin}
        className="w-full py-3 bg-[#5CC8FF] text-white font-bold rounded-lg hover:cursor-pointer transition-all flex items-center justify-center"
      >
        Login with Google
      </button>

      <button
        type="button"
        className="w-full py-3 bg-[#5CC8FF] hover:bg-[#4ab7e8] text-[#0D1821] font-bold rounded-lg transition-all"
      >
        <Link to="/home"> Login </Link>
      </button>
    </form>
  </div>
</div>

  );
};

export default LoginPage;
