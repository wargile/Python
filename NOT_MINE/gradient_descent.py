# http://spin.atomicobject.com/2014/06/24/gradient-descent-linear-regression/
# http://en.wikipedia.org/wiki/Stochastic_gradient_descent
# http://www.s-cool.co.uk/a-level/maths/differentiation/revise-it/the-chain-rule

# y = mx + b
# m is slope, b is y-intercept
def computeErrorForLineGivenPoints(b, m, points):
    totalError = 0
    for i in range(0, len(points)):
        totalError += (points[i].y - (m * points[i].x + b)) ** 2
    return totalError / float(len(points))

def stepGradient(b_current, m_current, points, learningRate):
    b_gradient = 0
    m_gradient = 0
    N = float(len(points))
    for i in range(0, len(points)):
        # This is the partial derivative.
        # TODO: Why -(2/N)? Because it's partial derivative of error funtion 1/N -  etc.?
        # Check the formulas at: http://en.wikipedia.org/wiki/Stochastic_gradient_descent
        b_gradient += -(2/N) * (points[i].y - ((m_current*points[i].x) + b_current))
        m_gradient += -(2/N) * points[i].x * (points[i].y - ((m_current * points[i].x) + b_current))
    new_b = b_current - (learningRate * b_gradient)
    new_m = m_current - (learningRate * m_gradient)
    return [new_b, new_m]

