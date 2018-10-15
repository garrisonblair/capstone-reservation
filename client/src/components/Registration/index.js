import axios from 'axios';
import React, {Component} from 'react';
import settings from '../../config/settings';
import './Registration.scss';
import {Form, Input, Button} from 'semantic-ui-react';

class Registration extends Component {

  state = {
    encsUsername: '',
    afterVerification: false
  }

  handleEncsUsername = (event) => {
    this.setState({encsUsername: event.target.value});
  }

  sendEmail = () => {
    const data = {"username": `${this.state.encsUsername}`};
    console.log(data);
    axios({
      method: 'POST',
      url: `${settings.API_ROOT}/register`,
      data: data
    })
      .then((response) => {
        console.log(response);
        this.setState({
          afterVerification: true
        });
      })
      .catch((error) => {
        if(error.message.includes('302')){
          console.log('302 error')
        }
        else if(error.message.includes('400')){
          console.log('400 error');
        }

      })
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
            <Button fluid size='small' icon onClick={this.sendEmail}>
              Send Email
            </Button>
          </Form.Field>
        </div>
      </div>
    )
  }
}

export default Registration;
