import React, {Component} from 'react';
import './Registration.scss';
import {Form, Input, Button} from 'semantic-ui-react';

class Registration extends Component {

  handleEncsUsername = () => {

  }

  render() {
    return (
      <div id="registration">
        <div className="container">
          <h1>Registration</h1>
          <p>Please enter your ENCS username. A validation will be sent to your email.</p>
          <Form.Field>
            <Input
              fluid
              size='small'
              icon='user'
              iconPosition='left'
              placeholder='ex. a_test'
              onChange={this.handleEncsUsername}
            />
          </Form.Field>
          <Form.Field>
            <br />
            <Button fluid size='small' icon onClick={this.handleLogin}>
              Send Email
            </Button>
          </Form.Field>
        </div>
      </div>
    )
  }
}

export default Registration;
