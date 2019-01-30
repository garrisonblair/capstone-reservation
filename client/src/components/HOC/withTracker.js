import React, { Component } from 'react';
import ReactGA from 'react-ga';
import settings from '../../config/settings';


function withTracker(WrappedComponent, options = {}) {
  const trackPage = (page) => {
    ReactGA.set({
      page,
      ...options,
    });
    ReactGA.pageview(page);
  };

  class HOC extends Component {
    componentDidMount() {
      const { location } = this.props;
      const page = location.pathname;
      trackPage(page);
    }

    componentWillReceiveProps(nextProps) {
      const { location } = this.props;
      const currentPage = location.pathname;
      const nextPage = nextProps.location.pathname;

      if (currentPage !== nextPage) {
        trackPage(nextPage);
      }
    }

    render() {
      return <WrappedComponent {...this.props} />;
    }
  }

  return settings.IS_PROD ? HOC : WrappedComponent;
}

export default withTracker;
