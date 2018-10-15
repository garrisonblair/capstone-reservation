import axios from 'axios';
import React, {Component} from 'react';
import './Registration.scss';
import {Form, Input, Button} from 'semantic-ui-react';

class Registration extends Component {

  state = {
    encsUsername:'',
    afterVerification: false
  }

  handleEncsUsername = () => {
    this.setState({encsUsername:event.target.value});
  }

  sendEmail = () => {
    console.log(this.props.match.params.token);
  }

  componentWillMount() {
    const {token} = this.props.match.params;
    const data = {"username":`${this.state.encsUsername}`};
    if (token) {
      axios({
        method: 'POST',
        url: `${settings.API_ROOT}/register`,
        data: data
      })
      .then((response) => {
        this.setState({
          afterVerification:true
        });
      })
      .catch((error) =>{

      })
    }
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
