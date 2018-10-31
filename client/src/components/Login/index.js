import React, {Component} from 'react';
import {Button, Form, Icon, Input} from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../utils/api';
import './Login.scss';
import {Link} from 'react-router-dom';


class Login extends Component {

  state = {
    username: '',
    password: ''
  }

  handleUsernameChange = (event) => {
    this.setState({username: event.target.value})
  }

  handlePasswordChange = (event) => {
    this.setState({password: event.target.value})
  }

  handleLogin = () => {
    const {history} = this.props;
    const {username, password} = this.state;

    api.login(username, password)
    .then((response) =>
      response.data
    )
    .then((data) => {
      localStorage.setItem('CapstoneReservationUser', JSON.stringify(data));
      history.push('/');
    })
    .catch((error) => {
      sweetAlert(
        ':(',
        'Invalid credentials',
        'error'
      )
    })
  }

  componentDidMount = () => {
    document.title = 'Login'
  }

  render = () => {
    const {showModal, modalType, modalTitle, modalText} = this.state;
    return (
      <div className="login login--center">
        <div className="login__container">
          <div className="login__container__header">
            <h1 className="login__container__header__title"> Login </h1>
          </div>
          <div className="login__container__main">
            <div className="ui divider"/>
            <div className="login__container__main__form-wrapper">
              <Form.Field>
                <Input
                  fluid
                  size='small'
                  icon='user'
                  iconPosition='left'
                  placeholder='Username'
                  onChange={this.handleUsernameChange}
                />
              </Form.Field>
              <Form.Field>
                <Input
                  fluid
                  size='small'
                  icon='lock'
                  iconPosition='left'
                  placeholder='Password'
                  type='password'
                  onChange={this.handlePasswordChange}
                />
              </Form.Field>
              <Form.Field>
                <Button fluid size='small' icon onClick={this.handleLogin}>
                  Login
                </Button>
              </Form.Field>
              <div className="ui divider"/>
              <span>First time? <Link to="/registration">Register!</Link></span>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Login;
