import axios from 'axios';
import settings from '../../config/settings';
import React, {Component} from 'react';
import './Verification.scss';
import {Loader, Icon, Step} from 'semantic-ui-react'


class Verification extends Component {
  state = {
    isLoading: true,
    firstName:''
  }
  componentWillMount() {
    const {token} = this.props.match.params;
    console.log(token);
    if (token) {
      const data = {"token": `${token}`}
      axios({
        method: 'POST',
        url: `${settings.API_ROOT}/verify`,
        data: data
      })
        .then((response) => {
          this.setState({
            isLoading: false,
            firstName: response.data.first_name
          });
          console.log(response);
        })
        .catch((error) => {
          console.log('verification failed')
        })
    }
  }

  render() {

    return (
      <div id="verification">
        <div className="container">
        <h1> Account settings </h1>
          <Step.Group size="mini" widths={2}>
            <Step completed>
              <Icon name="envelope" />
              <Step.Content>
                <Step.Title>Step 1</Step.Title>
                <Step.Description>ENCS username verification</Step.Description>
              </Step.Content>
            </Step>
            <Step active>
              <Icon name="cog" />
              <Step.Content>
                <Step.Title>Step 2</Step.Title>
                <Step.Description>Account setup</Step.Description>
              </Step.Content>
            </Step>
          </Step.Group>

          <Loader active inline='centered' active={this.state.isLoading} />

          <h3>Welcome {this.state.firstName}</h3>

        </div>

      </div>
    )
  }
}

export default Verification;
