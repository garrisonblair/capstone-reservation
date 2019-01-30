import React from 'react';
import renderer from 'react-test-renderer';
import Registration from '../../components/Registration/index';

it('Show registration', () => {
  const tree = renderer
    .create(<Registration />)
    .toJSON();
  expect(tree).toMatchSnapshot();
});

it('Show registration loader', () => {
  const tree = renderer
    .create(<Registration showLoaderForTest />)
    .toJSON();
  expect(tree).toMatchSnapshot();
});
