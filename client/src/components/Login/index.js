import React, {Component} from 'react';
import {Button, Form, Icon, Input} from 'semantic-ui-react'
import './Login.scss';


class Login extends Component {
  render() {
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
                <Input fluid size='small' icon='user' iconPosition='left' placeholder='Username' />
              </Form.Field>
              <Form.Field>
                <Input fluid size='small' icon='lock' iconPosition='left' placeholder='Password' type='password'/>
              </Form.Field>
              <Form.Field>
                <Button fluid size='small' icon>
                  Login
                </Button>
              </Form.Field>
              <div className="ui divider"/>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Login;
